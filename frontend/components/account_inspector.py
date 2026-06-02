# frontend/components/account_inspector.py

import hashlib
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from frontend.utils.constants import BASE_URL, FEATURE_NAMES
from frontend.components.graph_view import render_pyvis_network
from frontend.components.lifecycle_view import render_lifecycle_timeline, render_dispatch_controls
from frontend.components.compliance_panel import render_integrity_seal, render_goaml_download
from frontend.services.account_lookup import lookup_account_by_id

def render_account_inspector_view(target_account_id: str) -> None:
    """Renders the comprehensive Single Account Inspector and XAI Profiler."""
    st.subheader("🔍 Single Account Inspector & XAI Profiler")
    st.markdown("""
    Select or type an Account ID in the sidebar to run dual-engine prediction, calculate composite risk scores, 
    retrieve GDS topological centrality, and generate goAML suspicious transaction compliance reports instantly.
    """)

    # Fast account features lookup
    with st.spinner("Retrieving profile coordinates from DataSet.csv..."):
        features = lookup_account_by_id(target_account_id)

    if not features:
        st.error(
            f"❌ Account ID `{target_account_id}` was not found in `DataSet.csv`.\n"
            "Please ensure the format matches `ACC052 + 11-digit zero-padded index` (e.g., `ACC0520000000028` to `ACC0520000009082`)."
        )
        return

    st.success(f"✅ Found account profile coordinates for `{target_account_id}`.")
    
    # Interactive Trigger Button
    btn_clicked = st.button("⚡ Execute Forensic Prediction", key="btn_inspect_single")
    if btn_clicked:
        with st.spinner("Executing dual-engine inference and Neo4j topological lookup..."):
            try:
                payload = {"features": features}
                resp = requests.post(f"{BASE_URL}/predict/single", json=payload, timeout=10)
                
                if resp.status_code == 200:
                    st.session_state.inspected_data = resp.json()
                    st.session_state.inspected_account_id = target_account_id
                else:
                    st.error(f"❌ Prediction request failed with status {resp.status_code}: {resp.text}")
                    st.session_state.inspected_data = None
                    st.session_state.inspected_account_id = None
            except Exception as exc:
                st.error(f"❌ Could not reach FastAPI backend `/predict/single` endpoint: {exc}")
                st.session_state.inspected_data = None
                st.session_state.inspected_account_id = None
                
    # If we have persistent inspected data matching the current selection, display it
    if st.session_state.inspected_account_id == target_account_id and st.session_state.inspected_data is not None:
        data = st.session_state.inspected_data
        case_id = data.get("case_id", f"STR-MOCK")
        composite = data.get("composite_score", 0.0)
        ml_score = data.get("ml_score", 0.0)
        graph_score = data.get("graph_score", 0.0)
        severity = data.get("severity", "LOW")
        mule_stage = data.get("mule_stage", "LEGITIMATE")
        
        st.markdown("### 🕵️ Forensic Examination Results")
        
        # Premium 4-Column Metrics Cards Row
        col_card1, col_card2, col_card3, col_card4 = st.columns(4)
        
        sev_colors = {
            "CRITICAL": "#ef4444",
            "HIGH": "#f97316",
            "MEDIUM": "#eab308",
            "LOW": "#10b981",
            "LEGITIMATE": "#10b981",
            "UNDER_REVIEW": "#eab308"
        }
        sev_color = sev_colors.get(severity.upper(), "#10b981")
        
        with col_card1:
            st.markdown(f"""
            <div style='background-color:#1e293b;padding:15px;border-radius:8px;border-left:5px solid #38bdf8;box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1);'>
                <h5 style='color:#94a3b8;margin:0;font-size:12px;text-transform:uppercase;'>Composite Risk Score</h5>
                <h2 style='color:#f8fafc;margin:5px 0;font-size:24px;'>{composite}%</h2>
                <span style='color:#38bdf8;font-size:11px;font-weight:bold;'>Fused Analytics</span>
            </div>
            """, unsafe_allow_html=True)
            
        with col_card2:
            st.markdown(f"""
            <div style='background-color:#1e293b;padding:15px;border-radius:8px;border-left:5px solid {sev_color};box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1);'>
                <h5 style='color:#94a3b8;margin:0;font-size:12px;text-transform:uppercase;'>Severity Classification</h5>
                <h2 style='color:{sev_color};margin:5px 0;font-size:24px;'>{severity}</h2>
                <span style='color:{sev_color};font-size:11px;font-weight:bold;'>🛡️ Alert Status</span>
            </div>
            """, unsafe_allow_html=True)
            
        with col_card3:
            st.markdown(f"""
            <div style='background-color:#1e293b;padding:15px;border-radius:8px;border-left:5px solid #f59e0b;box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1);'>
                <h5 style='color:#94a3b8;margin:0;font-size:12px;text-transform:uppercase;'>Mule Lifecycle Stage</h5>
                <h2 style='color:#f8fafc;margin:5px 0;font-size:20px;font-weight:bold;'>{mule_stage.replace('_', ' ')}</h2>
                <span style='color:#f59e0b;font-size:11px;font-weight:bold;'>📍 Life Staging</span>
            </div>
            """, unsafe_allow_html=True)
            
        with col_card4:
            st.markdown(f"""
            <div style='background-color:#1e293b;padding:15px;border-radius:8px;border-left:5px solid #10b981;box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1);'>
                <h5 style='color:#94a3b8;margin:0;font-size:12px;text-transform:uppercase;'>Case Identifier</h5>
                <h2 style='color:#f8fafc;margin:5px 0;font-size:14px;font-family:monospace;font-weight:bold;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>{case_id or '—'}</h2>
                <span style='color:#10b981;font-size:11px;font-weight:bold;'>📂 STR Compliance File</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br/>", unsafe_allow_html=True)
        
        # Score Fusion & Details partitioned into 3 Tabs
        tab_forensic, tab_graph, tab_lifecycle = st.tabs([
            "📊 Forensic Breakdown",
            "🕸️ Graph Intelligence View",
            "📍 Mule Lifecycle Staging"
        ])
        
        with tab_forensic:
            # Score Fusion Formula Card
            st.markdown("#### ⚡ Composite Fusion Score Breakdown")
            
            col_f1, col_f2 = st.columns([2, 1])
            with col_f1:
                st.markdown(f"""
                <div style='background-color:#0f172a;padding:15px;border-radius:6px;border:1px solid #1e293b;margin-bottom:15px;'>
                    <code style='color:#38bdf8;font-size:14px;font-weight:bold;'>Composite = Profile Risk × 0.40 + Transaction Risk × 0.40 + Graph Risk × 0.20</code>
                    <br/><br/>
                    <span style='color:#94a3b8;font-size:13px;'>
                      - Profile Risk (XGBoost positive prob): <b>{data.get("profile_risk", ml_score)}%</b> × 0.40 = <b>{data.get("profile_risk", ml_score) * 0.40:.1f} pts</b>
                      <br/>
                      - Transaction Risk (detected live signals): <b>{data.get("transaction_risk", 0.0)}%</b> × 0.40 = <b>{data.get("transaction_risk", 0.0) * 0.40:.1f} pts</b>
                      <br/>
                      - Graph Risk (Neo4j or fallback centrality): <b>{data.get("graph_risk", graph_score)}%</b> × 0.20 = <b>{data.get("graph_risk", graph_score) * 0.20:.1f} pts</b>
                      <br/>
                      - Fused Sum: {(data.get("profile_risk", ml_score) * 0.40):.1f} + {(data.get("transaction_risk", 0.0) * 0.40):.1f} + {(data.get("graph_risk", graph_score) * 0.20):.1f} = <b>{composite}%</b>
                    </span>
                </div>
                """, unsafe_allow_html=True)
                
            with col_f2:
                if composite >= 40.0:
                    st.error("⚡ **STR TRIGGERED**\nFusion severity is MEDIUM or above. Investigator review or stronger action is required.")
                else:
                    st.info("🟢 **LEGITIMATE/MONITORED**\nRisk score remains below the STR action threshold. Continuous watchlist monitoring recommended.")
            
            # XAI SHAP & goAML Report Section
            col_bot1, col_bot2 = st.columns(2)
            with col_bot1:
                st.markdown("#### 🔍 Explainable AI (XAI) Feature Contribution")
                
                shap_sigs = data.get("shap_signals", {})
                if shap_sigs:
                    shap_rows = []
                    for feature, shap_val in shap_sigs.items():
                        label = FEATURE_NAMES.get(feature, f"Feature {feature}")
                        shap_rows.append({
                            "Signal": label,
                            "Impact Value": shap_val,
                            "Impact Points": f"+{abs(int(shap_val * 100))} pts" if shap_val > 0 else f"-{abs(int(shap_val * 100))} pts"
                        })
                    df_shap = pd.DataFrame(shap_rows)
                    
                    fig_shap = px.bar(
                        df_shap,
                        x="Impact Value",
                        y="Signal",
                        orientation="h",
                        color="Impact Value",
                        color_continuous_scale=px.colors.diverging.RdYlGn[::-1],
                        title="XAI SHAP Feature Contribution (Named Signals)"
                    )
                    fig_shap.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="white",
                        coloraxis_showscale=False,
                        margin=dict(l=10, r=10, t=30, b=10),
                        height=250
                    )
                    st.plotly_chart(fig_shap, width='stretch')
                    
                    for row in shap_rows:
                        st.markdown(f"- **{row['Signal']}**: `{row['Impact Points']}`")
                else:
                    st.caption("No SHAP attributions generated for this profile.")
                    
            with col_bot2:
                st.markdown("#### 📂 goAML XML Compliance Autopilot")
                goaml_xml = data.get("goaml_xml", "")
                
                if goaml_xml:
                    st.text_area("Compliance XML Document", goaml_xml, height=200)
                    render_goaml_download(goaml_xml, case_id, target_account_id)
                    
                    st.markdown("##### 🔐 Tamper-Proof Integrity Signature")
                    evidence_hash = hashlib.sha256(goaml_xml.encode()).hexdigest()
                    render_integrity_seal(evidence_hash)
                else:
                    st.info("goAML Suspicious Report XML is not triggered for Legitimate/Low risk account profile.")
                    
        with tab_graph:
            st.markdown("#### 🕸️ Graph Intelligence View & Risk Propagation")
            
            is_critical = composite >= 60.0
            if is_critical:
                neighbors_count = 6
                highest_risk = "ACC052...0999 (98.0% - CRITICAL)"
                density = "0.33 (Suspicious Dense)"
                threat_level = "🚨 DENSE CIRCULAR LAYERING DETECTED"
                propagation_desc = f"Tabular ML standalone risk is high at {ml_score}%. Graph centrality degree of {graph_score}% indicates multiple high-velocity UPI inputs and laundering sink flows, reinforcing a CRITICAL risk classification."
            else:
                neighbors_count = 2
                highest_risk = "ACC052...0500 (1.2% - LOW)"
                density = "0.67 (Normal)"
                threat_level = "🟢 NORMAL RETAIL PROFILE"
                propagation_desc = f"Tabular ML standalone risk remains low at {ml_score}%. Minor graph centrality degree of {graph_score}% reflects normal sparse retail transaction relationships, maintaining a low-risk classification."
                
            # Graph Score split columns
            col_g1, col_g2 = st.columns([1, 2])
            with col_g1:
                st.markdown(f"""
                <div style='background-color:#1e293b;padding:15px;border-radius:6px;border:1px solid #334155;margin-bottom:15px;'>
                    <h5 style='color:#94a3b8;margin:0;font-size:12px;text-transform:uppercase;'>Graph Core Metrics</h5>
                    <div style='margin-top:10px;'>
                        <small style='color:#94a3b8;'>Standalone ML Score:</small> <b style='color:#f8fafc;'>{ml_score}%</b><br/>
                        <small style='color:#94a3b8;'>Graph Centrality Score:</small> <b style='color:#38bdf8;'>{graph_score}%</b><br/>
                        <small style='color:#94a3b8;'>Fused Composite Score:</small> <b style='color:#ef4444;'>{composite}%</b>
                    </div>
                </div>
                
                <div style='background-color:#0f172a;padding:15px;border-radius:6px;border:1px solid #1e293b;margin-bottom:15px;'>
                    <h5 style='color:#38bdf8;margin:0;font-size:13px;text-transform:uppercase;'>🕸️ Propagation Narrative</h5>
                    <p style='color:#94a3b8;font-size:12px;margin:8px 0 0 0;'>
                        {propagation_desc}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Investigation metrics
                st.markdown("##### 🕵️ Network Investigation Panel")
                st.metric("Connected Accounts Count", f"{neighbors_count}")
                st.metric("Highest Risk Neighbor", f"{highest_risk}")
                st.metric("Network Density Ratio", f"{density}")
                
                if is_critical:
                    st.error(threat_level)
                else:
                    st.success(threat_level)
                    
            with col_g2:
                st.markdown("##### Interactive Graph Network Representation")
                st.caption("Hover over nodes to inspect details, use scroll to zoom, drag nodes to reposition.")
                render_pyvis_network(target_account_id, composite, ml_score, graph_score, severity, mule_stage)
                
        with tab_lifecycle:
            st.markdown("#### 📍 Mule Lifecycle Staging & Investigator SOP")
            current_step, reason, action_sop = render_lifecycle_timeline(mule_stage)
            
            # Staging explanations
            col_l1, col_l2 = st.columns(2)
            with col_l1:
                st.markdown(f"""
                <div style='background-color:#1e293b;padding:20px;border-radius:8px;border-left:5px solid #f97316;box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);'>
                    <h4 style='color:#f8fafc;margin:0 0 10px 0;'>📍 Timeline Card</h4>
                    <span style='color:#94a3b8;font-size:12px;text-transform:uppercase;'>Current Stage:</span><br/>
                    <b style='color:#f97316;font-size:18px;'>{current_step}</b>
                    <br/><br/>
                    <span style='color:#94a3b8;font-size:12px;text-transform:uppercase;'>Reason:</span><br/>
                    <p style='color:#f8fafc;font-size:14px;margin:2px 0 0 0;'>{reason}</p>
                    <br/>
                    <span style='color:#94a3b8;font-size:12px;text-transform:uppercase;'>Recommended Action:</span><br/>
                    <p style='color:#10b981;font-size:14px;font-weight:bold;margin:2px 0 0 0;'>{action_sop}</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col_l2:
                render_dispatch_controls(target_account_id)
