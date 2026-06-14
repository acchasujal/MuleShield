# frontend/components/demo_mode.py

import pandas as pd
import streamlit as st

def render_threat_simulation_view(load_scenario_callback) -> None:
    """Renders the Threat Simulation Library — pre-loaded AML investigation datasets."""

    st.subheader("Threat Simulation Library")
    st.caption("Pre-loaded transaction intelligence datasets representing documented AML laundering patterns. Select a pattern to ingest and activate the investigation workspace.")

    # Active dataset indicator
    active_scenario = st.session_state.get("active_scenario")
    if active_scenario and st.session_state.analysis_result is not None:
        scenario_labels = {
            "dormant_reactivation": ("Dormant Reactivation Ring",    "#ef4444"),
            "student_recruitment":  ("Student Mule Recruitment",     "#f97316"),
            "agri_diversion":       ("Agri Subsidy Diversion",       "#ef4444"),
        }
        lbl, clr = scenario_labels.get(active_scenario, ("Unknown", "#94a3b8"))
        alerts_loaded = len(st.session_state.analysis_result.get("alerts", []))
        st.markdown(f"""
        <div style='background-color:#0f172a;padding:12px 18px;border-radius:6px;border-left:4px solid {clr};margin-bottom:20px;display:flex;align-items:center;gap:12px;'>
            <div style='width:8px;height:8px;border-radius:50%;background:{clr};flex-shrink:0;'></div>
            <div>
                <span style='color:#f8fafc;font-weight:600;font-size:14px;'>{lbl} — Dataset Active</span><br/>
                <span style='color:#94a3b8;font-size:12px;'>{alerts_loaded} accounts flagged. Navigate to Alerts to begin investigation.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        col_go1, _ = st.columns([1, 3])
        with col_go1:
            if st.button("Open Alert Queue", key="demo_goto_alerts", use_container_width=True):
                st.session_state.demo_mode_active = True
                st.rerun()

    st.markdown("#### Select Simulation Pattern")

    # Scenario Cards
    col_d1, col_d2, col_d3 = st.columns(3)

    with col_d1:
        st.markdown("""
        <div style='background:#0f172a;padding:20px;border-radius:8px;border:1px solid #334155;border-top:3px solid #ef4444;min-height:260px;'>
            <div style='display:flex;align-items:center;gap:8px;margin-bottom:10px;'>
                <span style='background:#ef4444;color:#fff;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700;letter-spacing:0.05em;'>HIGH</span>
                <span style='color:#64748b;font-size:10px;'>Dormancy · G365D Reactivation</span>
            </div>
            <h4 style='color:#f8fafc;margin:0 0 8px 0;font-size:15px;font-weight:600;'>Dormant Reactivation Ring</h4>
            <p style='color:#94a3b8;font-size:12px;line-height:1.6;margin-bottom:14px;'>
                A 3.5-year dormant savings account is reactivated via social engineering for high-volume NEFT pass-through to a mule aggregator, cashing out via a UPI layering ring.
            </p>
            <div style='background:#1e293b;padding:10px 12px;border-radius:4px;margin-bottom:8px;'>
                <div style='color:#ef4444;font-size:10px;font-weight:700;text-transform:uppercase;margin-bottom:4px;letter-spacing:0.05em;'>Transaction Pattern</div>
                <div style='color:#94a3b8;font-size:11px;line-height:1.7;font-family:monospace;'>
                    G365D Dormant Account<br/>
                    ↓ Reactivation NEFTs<br/>
                    Mule Aggregator Node<br/>
                    ↓ 4-Node Fan-Out
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Load Dormant Pattern", key="dm_launch_dormant_ring", use_container_width=True):
            with st.spinner("Loading Dormant Reactivation dataset..."):
                load_scenario_callback("data/scenario_dormant_reactivation.csv", "scenario_dormant_reactivation.csv")
            st.session_state.demo_mode_active = True
            st.rerun()

    with col_d2:
        st.markdown("""
        <div style='background:#0f172a;padding:20px;border-radius:8px;border:1px solid #334155;border-top:3px solid #f97316;min-height:260px;'>
            <div style='display:flex;align-items:center;gap:8px;margin-bottom:10px;'>
                <span style='background:#f97316;color:#fff;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700;letter-spacing:0.05em;'>MEDIUM</span>
                <span style='color:#64748b;font-size:10px;'>Student Mule Network</span>
            </div>
            <h4 style='color:#f8fafc;margin:0 0 8px 0;font-size:15px;font-weight:600;'>Student Mule Recruitment</h4>
            <p style='color:#94a3b8;font-size:12px;line-height:1.6;margin-bottom:14px;'>
                College students recruited via social media. Controller seeds accounts via UPI over 77 minutes to evade velocity limits, funnelling through layering node.
            </p>
            <div style='background:#1e293b;padding:10px 12px;border-radius:4px;margin-bottom:8px;'>
                <div style='color:#f97316;font-size:10px;font-weight:700;text-transform:uppercase;margin-bottom:4px;letter-spacing:0.05em;'>Transaction Pattern</div>
                <div style='color:#94a3b8;font-size:11px;line-height:1.7;font-family:monospace;'>
                    Recruiter Controller<br/>
                    ↓ UPI × 6<br/>
                    6 Student Mules<br/>
                    ↓ Layering Exit
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Load Student Pattern", key="dm_launch_student", use_container_width=True):
            with st.spinner("Loading Student Recruitment dataset..."):
                load_scenario_callback("data/scenario_student_recruitment.csv", "scenario_student_recruitment.csv")
            st.session_state.demo_mode_active = True
            st.rerun()

    with col_d3:
        st.markdown("""
        <div style='background:#0f172a;padding:20px;border-radius:8px;border:1px solid #334155;border-top:3px solid #ef4444;min-height:260px;'>
            <div style='display:flex;align-items:center;gap:8px;margin-bottom:10px;'>
                <span style='background:#ef4444;color:#fff;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700;letter-spacing:0.05em;'>HIGH</span>
                <span style='color:#64748b;font-size:10px;'>Subsidy Diversion</span>
            </div>
            <h4 style='color:#f8fafc;margin:0 0 8px 0;font-size:15px;font-weight:600;'>Agri Subsidy Diversion</h4>
            <p style='color:#94a3b8;font-size:12px;line-height:1.6;margin-bottom:14px;'>
                PM-Kisan DBT disbursements meant for 10 rural farmers in Aurangabad are diverted to an aggregator, then layered through Pune to a Mumbai shell entity.
            </p>
            <div style='background:#1e293b;padding:10px 12px;border-radius:4px;margin-bottom:8px;'>
                <div style='color:#ef4444;font-size:10px;font-weight:700;text-transform:uppercase;margin-bottom:4px;letter-spacing:0.05em;'>Transaction Pattern</div>
                <div style='color:#94a3b8;font-size:11px;line-height:1.7;font-family:monospace;'>
                    10× PM-Kisan DBT<br/>
                    ↓ Immediate Diversion<br/>
                    Pune/Mumbai Layering<br/>
                    ↓ Shell Entity RTGS
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Load Agri Pattern", key="dm_launch_agri", use_container_width=True):
            with st.spinner("Loading Agri Subsidy dataset..."):
                load_scenario_callback("data/scenario_agri_diversion.csv", "scenario_agri_diversion.csv")
            st.session_state.demo_mode_active = True
            st.rerun()

    st.markdown("<br/>", unsafe_allow_html=True)

    # Inline results preview when scenario is loaded
    if st.session_state.analysis_result is not None:
        st.markdown("---")
        st.markdown("#### Analysis Results")
        result = st.session_state.analysis_result
        alerts = result.get("alerts", [])
        flagged = result.get("flagged_count", len(alerts))
        total = result.get("total_analyzed", flagged)

        prv1, prv2, prv3, prv4 = st.columns(4)
        prv1.metric("Accounts Analyzed", f"{total:,}")
        prv2.metric("Flagged Alerts", f"{flagged:,}")
        critical_c = sum(1 for a in alerts if a.get("severity") == "CRITICAL")
        prv3.metric("Critical Escalations", f"{critical_c:,}")
        prv4.metric("Detection Latency", "< 8 sec", "SLA compliant")

        if alerts:
            st.markdown("#### Top Flagged Accounts")
            top_rows = []
            for a in alerts[:6]:
                top_rows.append({
                    "Account ID":    a.get("account", "—"),
                    "Risk Score":    f"{a.get('risk_score', 0)}%",
                    "Severity":      a.get("severity", "LOW"),
                    "Lifecycle Stage": a.get("mule_stage", "LEGITIMATE"),
                })
            st.dataframe(pd.DataFrame(top_rows), use_container_width=True)

        col_nav_d1, col_nav_d2 = st.columns(2)
        with col_nav_d1:
            st.info("Navigate to **Alerts** in the sidebar to review full forensic investigations.")
        with col_nav_d2:
            st.info("Navigate to **Accounts** to run deep risk profiling on individual accounts.")
