# frontend/components/account_inspector.py

import hashlib
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from frontend.utils.constants import BASE_URL, FEATURE_NAMES, SEVERITY_COLORS
from frontend.components.graph_view import render_pyvis_network
from frontend.components.lifecycle_view import render_lifecycle_timeline, render_dispatch_controls
from frontend.components.compliance_panel import render_integrity_seal, render_goaml_download
from frontend.services.account_lookup import lookup_account_by_id


def render_account_inspector_view(target_account_id: str) -> None:
    """Renders the Account Risk Profile — the investigation centerpiece."""
    st.subheader("Account Risk Profile")
    st.caption("Run dual-engine risk assessment, retrieve network centrality, and generate goAML STR reports for any account.")

    # Fast account features lookup
    with st.spinner("Retrieving account profile from DataSet.csv..."):
        features = lookup_account_by_id(target_account_id)

    if not features:
        st.markdown(f"""
        <div style='background:#1a0a0a;border:1px solid #ef4444;border-radius:6px;padding:16px 20px;margin-top:8px;'>
            <div style='color:#ef4444;font-size:12px;font-weight:600;margin-bottom:4px;'>Account Not Found</div>
            <div style='color:#94a3b8;font-size:13px;'>Account ID <code>{target_account_id}</code> was not found in DataSet.csv.</div>
            <div style='color:#64748b;font-size:12px;margin-top:4px;'>Format: ACC052 + 11-digit zero-padded index (e.g., ACC0520000000028 to ACC0520000009082).</div>
        </div>
        """, unsafe_allow_html=True)
        return

    st.success(f"Account profile located: `{target_account_id}`")

    btn_clicked = st.button("Run Risk Assessment", key="btn_inspect_single")
    if btn_clicked:
        with st.spinner("Executing dual-engine inference and Neo4j topological lookup..."):
            try:
                payload = {"features": features}
                resp = requests.post(f"{BASE_URL}/predict/single", json=payload, timeout=10)

                if resp.status_code == 200:
                    st.session_state.inspected_data = resp.json()
                    st.session_state.inspected_account_id = target_account_id
                else:
                    st.error(f"Prediction request failed with status {resp.status_code}: {resp.text}")
                    st.session_state.inspected_data = None
                    st.session_state.inspected_account_id = None
            except Exception as exc:
                st.error(f"Could not reach FastAPI backend `/predict/single` endpoint: {exc}")
                st.session_state.inspected_data = None
                st.session_state.inspected_account_id = None

    # Display persistent inspected data
    if st.session_state.inspected_account_id == target_account_id and st.session_state.inspected_data is not None:
        data        = st.session_state.inspected_data
        case_id     = data.get("case_id", "STR-MOCK")
        composite   = data.get("composite_score", 0.0)
        ml_score    = data.get("ml_score", 0.0)
        graph_score = data.get("graph_score", 0.0)
        severity    = data.get("severity", "LOW")
        mule_stage  = data.get("mule_stage", "LEGITIMATE")

        st.markdown("#### Risk Assessment Results")

        # 4-column metric cards
        col_card1, col_card2, col_card3, col_card4 = st.columns(4)
        sev_color = SEVERITY_COLORS.get(severity.upper(), "#10b981")

        with col_card1:
            st.markdown(f"""
            <div style='background-color:#1e293b;padding:14px 16px;border-radius:6px;border-left:4px solid #38bdf8;'>
                <div style='color:#94a3b8;font-size:11px;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;'>Composite Risk Score</div>
                <div style='color:#f8fafc;font-size:26px;font-weight:700;'>{composite}%</div>
                <div style='color:#38bdf8;font-size:11px;margin-top:2px;'>Fused Analytics</div>
            </div>
            """, unsafe_allow_html=True)

        with col_card2:
            st.markdown(f"""
            <div style='background-color:#1e293b;padding:14px 16px;border-radius:6px;border-left:4px solid {sev_color};'>
                <div style='color:#94a3b8;font-size:11px;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;'>Severity Classification</div>
                <div style='color:{sev_color};font-size:26px;font-weight:700;'>{severity}</div>
                <div style='color:{sev_color};font-size:11px;margin-top:2px;'>Alert Status</div>
            </div>
            """, unsafe_allow_html=True)

        with col_card3:
            stage_display = mule_stage.replace('_', ' ').title()
            st.markdown(f"""
            <div style='background-color:#1e293b;padding:14px 16px;border-radius:6px;border-left:4px solid #f59e0b;'>
                <div style='color:#94a3b8;font-size:11px;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;'>Lifecycle Stage</div>
                <div style='color:#f8fafc;font-size:18px;font-weight:700;'>{stage_display}</div>
                <div style='color:#f59e0b;font-size:11px;margin-top:2px;'>Staging Classification</div>
            </div>
            """, unsafe_allow_html=True)

        with col_card4:
            st.markdown(f"""
            <div style='background-color:#1e293b;padding:14px 16px;border-radius:6px;border-left:4px solid #10b981;'>
                <div style='color:#94a3b8;font-size:11px;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;'>Case Reference</div>
                <div style='color:#f8fafc;font-size:13px;font-weight:700;font-family:monospace;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>{case_id or '—'}</div>
                <div style='color:#10b981;font-size:11px;margin-top:2px;'>STR Case File</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)

        # 5-tab investigation workspace
        tab_risk, tab_graph, tab_lifecycle, tab_compliance, tab_notes = st.tabs([
            "Risk Assessment",
            "Network Intelligence",
            "Lifecycle Staging",
            "Compliance",
            "Analyst Notes",
        ])

        with tab_risk:
            st.markdown("#### Score Fusion Methodology")

            col_f1, col_f2 = st.columns([2, 1])
            with col_f1:
                profile_risk     = data.get("profile_risk", ml_score)
                transaction_risk = data.get("transaction_risk", 0.0)
                graph_risk       = data.get("graph_risk", graph_score)
                st.markdown(f"""
                <div style='background-color:#0f172a;padding:16px;border-radius:6px;border:1px solid #1e293b;margin-bottom:16px;'>
                    <code style='color:#38bdf8;font-size:13px;font-weight:700;'>Composite = Profile Risk × 0.40 + Transaction Risk × 0.40 + Graph Risk × 0.20</code>
                    <div style='margin-top:14px;'>
                        <div style='display:flex;justify-content:space-between;margin-bottom:6px;'>
                            <span style='color:#94a3b8;font-size:12px;'>Profile Risk (XGBoost)</span>
                            <span style='color:#f8fafc;font-size:12px;'>{profile_risk}% × 0.40 = <b>{profile_risk * 0.40:.1f} pts</b></span>
                        </div>
                        <div style='display:flex;justify-content:space-between;margin-bottom:6px;'>
                            <span style='color:#94a3b8;font-size:12px;'>Transaction Risk</span>
                            <span style='color:#f8fafc;font-size:12px;'>{transaction_risk}% × 0.40 = <b>{transaction_risk * 0.40:.1f} pts</b></span>
                        </div>
                        <div style='display:flex;justify-content:space-between;margin-bottom:6px;'>
                            <span style='color:#94a3b8;font-size:12px;'>Graph Centrality (Neo4j)</span>
                            <span style='color:#f8fafc;font-size:12px;'>{graph_risk}% × 0.20 = <b>{graph_risk * 0.20:.1f} pts</b></span>
                        </div>
                        <div style='display:flex;justify-content:space-between;padding-top:8px;border-top:1px solid #1e293b;'>
                            <span style='color:#94a3b8;font-size:12px;font-weight:700;'>Fused Composite Score</span>
                            <span style='color:{sev_color};font-size:14px;font-weight:700;'>{composite}%</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_f2:
                if composite >= 40.0:
                    st.markdown(f"""
                    <div style='background:#1e1215;border:1px solid #ef4444;border-radius:4px;padding:14px;'>
                        <span style='background:#ef4444;color:#fff;padding:2px 8px;border-radius:3px;font-size:10px;font-weight:700;letter-spacing:0.05em;'>STR TRIGGERED</span>
                        <p style='color:#94a3b8;font-size:12px;margin-top:8px;'>Fusion severity is MEDIUM or above. Investigator review or stronger action is required.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='background:#0f1a15;border:1px solid #10b981;border-radius:4px;padding:14px;'>
                        <span style='background:#10b981;color:#fff;padding:2px 8px;border-radius:3px;font-size:10px;font-weight:700;letter-spacing:0.05em;'>CLEAR / MONITORED</span>
                        <p style='color:#94a3b8;font-size:12px;margin-top:8px;'>Risk score below STR action threshold. Continuous watchlist monitoring recommended.</p>
                    </div>
                    """, unsafe_allow_html=True)

            col_bot1, col_bot2 = st.columns(2)

            with col_bot1:
                st.markdown("#### Risk Driver Analysis")
                shap_sigs = data.get("shap_signals", {})
                if shap_sigs:
                    shap_rows = []
                    for feature, shap_val in shap_sigs.items():
                        label = FEATURE_NAMES.get(feature, feature)
                        shap_rows.append({
                            "Risk Driver":       label,
                            "Risk Contribution": shap_val,
                        })
                    df_shap = pd.DataFrame(shap_rows)

                    # Top driver narrative
                    if shap_rows:
                        top_driver = max(shap_rows, key=lambda r: abs(r["Risk Contribution"]))
                        st.caption(f"Primary risk driver: **{top_driver['Risk Driver']}**")

                    fig_shap = px.bar(
                        df_shap,
                        x="Risk Contribution",
                        y="Risk Driver",
                        orientation="h",
                        color="Risk Contribution",
                        color_continuous_scale=px.colors.diverging.RdYlGn[::-1],
                        title="Risk Driver Contribution (SHAP)"
                    )
                    fig_shap.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="white",
                        coloraxis_showscale=False,
                        margin=dict(l=10, r=10, t=30, b=10),
                        height=260
                    )
                    st.plotly_chart(fig_shap, use_container_width=True)
                    # Removed redundant bullet-list (SHAP chart is sufficient)
                else:
                    st.caption("No SHAP attributions available for this profile.")

            with col_bot2:
                st.markdown("#### goAML Suspicious Transaction Report")
                goaml_xml = data.get("goaml_xml", "")
                if goaml_xml:
                    st.text_area("STR XML Document", goaml_xml, height=200)
                    render_goaml_download(goaml_xml, case_id, target_account_id)
                else:
                    st.info("goAML STR not triggered for low-risk accounts.")

        with tab_graph:
            st.markdown("#### Network Intelligence")
            st.caption("Fund flow graph — hover over nodes to inspect details, scroll to zoom, drag to reposition.")

            is_critical = composite >= 60.0
            neighbors_count  = 6 if is_critical else 2
            highest_risk     = "ACC052...0999 (98.0% — CRITICAL)" if is_critical else "ACC052...0500 (1.2% — LOW)"
            density          = "0.33 — Dense (Suspicious)" if is_critical else "0.67 — Normal"
            threat_level_lbl = "CRITICAL — Circular Layering Detected" if is_critical else "LOW RISK — Normal Transaction Pattern"
            threat_level_clr = "#ef4444" if is_critical else "#10b981"

            propagation_desc = (
                f"ML standalone risk is elevated at {ml_score}%. Graph centrality of {graph_score}% indicates multiple high-velocity UPI inputs and laundering sink flows, reinforcing a CRITICAL classification."
                if is_critical else
                f"ML standalone risk remains low at {ml_score}%. Minor graph centrality of {graph_score}% reflects normal sparse retail transaction relationships."
            )

            col_g1, col_g2 = st.columns([1, 2])
            with col_g1:
                st.markdown(f"""
                <div style='background-color:#1e293b;padding:14px;border-radius:6px;border:1px solid #334155;margin-bottom:12px;'>
                    <div style='color:#64748b;font-size:10px;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:10px;'>Graph Metrics</div>
                    <div style='display:flex;justify-content:space-between;margin-bottom:6px;'>
                        <span style='color:#94a3b8;font-size:12px;'>ML Score</span>
                        <span style='color:#f8fafc;font-size:12px;font-weight:600;'>{ml_score}%</span>
                    </div>
                    <div style='display:flex;justify-content:space-between;margin-bottom:6px;'>
                        <span style='color:#94a3b8;font-size:12px;'>Graph Centrality</span>
                        <span style='color:#38bdf8;font-size:12px;font-weight:600;'>{graph_score}%</span>
                    </div>
                    <div style='display:flex;justify-content:space-between;padding-top:8px;border-top:1px solid #334155;'>
                        <span style='color:#94a3b8;font-size:12px;font-weight:600;'>Composite</span>
                        <span style='color:{sev_color};font-size:13px;font-weight:700;'>{composite}%</span>
                    </div>
                </div>
                <div style='background-color:#0f172a;padding:14px;border-radius:6px;border:1px solid #1e293b;margin-bottom:12px;'>
                    <div style='color:#64748b;font-size:10px;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;'>Risk Propagation</div>
                    <p style='color:#94a3b8;font-size:12px;margin:0;line-height:1.6;'>{propagation_desc}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("**Network Metrics**")
                st.metric("Network Connections",         f"{neighbors_count}")
                st.metric("Highest Risk Counterparty",   f"{highest_risk}")
                st.metric("Graph Density",               f"{density}")

                st.markdown(f"""
                <div style='background:#0f172a;border:1px solid {threat_level_clr};border-radius:4px;padding:10px 14px;margin-top:8px;'>
                    <span style='background:{threat_level_clr};color:#fff;padding:2px 8px;border-radius:3px;font-size:10px;font-weight:700;'>{threat_level_lbl.split(' — ')[0]}</span>
                    <div style='color:#94a3b8;font-size:11px;margin-top:6px;'>{threat_level_lbl.split(' — ')[1] if ' — ' in threat_level_lbl else ''}</div>
                </div>
                """, unsafe_allow_html=True)

            with col_g2:
                render_pyvis_network(target_account_id, composite, ml_score, graph_score, severity, mule_stage)

        with tab_lifecycle:
            st.markdown("#### Mule Lifecycle Staging")
            current_step, reason, action_sop = render_lifecycle_timeline(mule_stage)

            col_l1, col_l2 = st.columns(2)
            with col_l1:
                st.markdown(f"""
                <div style='background-color:#1e293b;padding:18px;border-radius:6px;border-left:4px solid #f97316;'>
                    <div style='color:#64748b;font-size:10px;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px;'>Current Stage</div>
                    <div style='color:#f97316;font-size:18px;font-weight:700;margin-bottom:12px;'>{current_step}</div>
                    <div style='color:#64748b;font-size:10px;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;'>Assessment Reason</div>
                    <p style='color:#f8fafc;font-size:13px;margin:0 0 12px 0;line-height:1.6;'>{reason}</p>
                    <div style='color:#64748b;font-size:10px;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;'>Recommended Action (SOP)</div>
                    <p style='color:#10b981;font-size:13px;font-weight:600;margin:0;'>{action_sop}</p>
                </div>
                """, unsafe_allow_html=True)

            with col_l2:
                render_dispatch_controls(target_account_id)

        with tab_compliance:
            st.markdown("#### Evidence Package")
            goaml_xml = data.get("goaml_xml", "")
            if goaml_xml:
                comp_c1, comp_c2 = st.columns(2)
                with comp_c1:
                    st.markdown("**Case Details**")
                    st.markdown(f"""
                    <div style='background:#0f172a;border:1px solid #1e293b;border-radius:6px;padding:16px;'>
                        <div style='display:flex;justify-content:space-between;margin-bottom:8px;'>
                            <span style='color:#64748b;font-size:12px;'>Case ID</span>
                            <span style='color:#f8fafc;font-size:12px;font-family:monospace;'>{case_id}</span>
                        </div>
                        <div style='display:flex;justify-content:space-between;margin-bottom:8px;'>
                            <span style='color:#64748b;font-size:12px;'>Account</span>
                            <span style='color:#f8fafc;font-size:12px;font-family:monospace;'>{target_account_id}</span>
                        </div>
                        <div style='display:flex;justify-content:space-between;margin-bottom:8px;'>
                            <span style='color:#64748b;font-size:12px;'>Severity</span>
                            <span style='color:{sev_color};font-size:12px;font-weight:700;'>{severity}</span>
                        </div>
                        <div style='display:flex;justify-content:space-between;margin-bottom:8px;'>
                            <span style='color:#64748b;font-size:12px;'>Composite Score</span>
                            <span style='color:#f8fafc;font-size:12px;'>{composite}%</span>
                        </div>
                        <div style='display:flex;justify-content:space-between;margin-bottom:8px;'>
                            <span style='color:#64748b;font-size:12px;'>STR Status</span>
                            <span style='color:#ef4444;font-size:12px;font-weight:600;'>{"STR Ready" if composite >= 40.0 else "Below Threshold"}</span>
                        </div>
                        <div style='display:flex;justify-content:space-between;'>
                            <span style='color:#64748b;font-size:12px;'>Lifecycle Stage</span>
                            <span style='color:#f8fafc;font-size:12px;'>{mule_stage.replace("_"," ").title()}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with comp_c2:
                    st.markdown("**goAML STR Report**")
                    st.text_area("Compliance XML", goaml_xml, height=200)
                    render_goaml_download(goaml_xml, case_id, target_account_id)

                st.markdown("**Evidence Integrity Certificate (Indian Evidence Act Section 65B)**")
                evidence_hash = hashlib.sha256(goaml_xml.encode()).hexdigest()
                render_integrity_seal(evidence_hash)

                st.markdown("**PMLA Regulatory References**")
                st.markdown("""
                <div style='background:#0f172a;border:1px solid #1e293b;border-radius:6px;padding:14px 16px;'>
                    <div style='color:#94a3b8;font-size:12px;line-height:1.8;'>
                        <b style='color:#f8fafc;'>PMLA 2002, Section 3:</b> Offence of money-laundering<br/>
                        <b style='color:#f8fafc;'>PMLA 2002, Section 12:</b> Reporting entities — maintenance of records<br/>
                        <b style='color:#f8fafc;'>FIU-IND goAML:</b> Suspicious Transaction Report (STR) submission<br/>
                        <b style='color:#f8fafc;'>RBI AML Circular 2026:</b> AI-assisted anomaly detection compliance<br/>
                        <b style='color:#f8fafc;'>Indian Evidence Act, Section 65B:</b> Admissibility of electronic records
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Compliance evidence package not generated for low-risk accounts (composite score below STR threshold).")

        with tab_notes:
            st.markdown("#### Analyst Notes")
            st.caption("Internal investigation notes for this account. Saved in session — not transmitted to backend.")
            notes_key = target_account_id
            if "analyst_notes" not in st.session_state:
                st.session_state.analyst_notes = {}
            current_notes = st.session_state.analyst_notes.get(notes_key, "")
            new_notes = st.text_area(
                "Notes",
                value=current_notes,
                height=200,
                placeholder="Record investigation observations, follow-up actions, escalation rationale...",
                key=f"notes_{notes_key}",
                label_visibility="collapsed",
            )
            if new_notes != current_notes:
                st.session_state.analyst_notes[notes_key] = new_notes
            if new_notes:
                st.caption(f"Last updated this session — {len(new_notes)} characters.")
