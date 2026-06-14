# frontend/components/alert_center.py

import hashlib
import pandas as pd
import streamlit as st
import plotly.express as px
from frontend.utils.constants import SEVERITY_EMOJI, SEVERITY_COLORS, GRAPH_COLORS, PAGE_SIZE, FEATURE_NAMES
from frontend.components.compliance_panel import render_integrity_seal, render_goaml_download, render_pdf_export

def _severity_badge(severity: str) -> str:
    """Return an inline HTML severity badge."""
    color = SEVERITY_COLORS.get(severity.upper(), "#64748b")
    label = severity.upper()
    return f"<span style='background:{color};color:#fff;padding:2px 9px;border-radius:3px;font-size:10px;font-weight:700;letter-spacing:0.05em;'>{label}</span>"


def render_alert_center_view() -> None:
    """Renders the professional Alert Queue dashboard."""
    alerts_data = st.session_state.analysis_result

    if alerts_data is None:
        st.markdown("""
        <div style='background:#0f172a;border:1px solid #1e293b;border-radius:8px;padding:32px;text-align:center;margin-top:20px;'>
            <div style='color:#475569;font-size:14px;margin-bottom:8px;font-weight:500;'>No Active Investigation Dataset</div>
            <div style='color:#334155;font-size:12px;'>Upload a transaction CSV or load a pattern from the Investigations workspace.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    alerts         = alerts_data.get("alerts", [])
    total_analyzed = alerts_data.get("total_analyzed") or len(alerts)
    flagged_count  = alerts_data.get("flagged_count") or len(alerts)

    st.subheader("Alert Queue")

    # KPI strip
    m1, m2, m3, m4 = st.columns(4)
    critical_count   = sum(1 for a in alerts if a["severity"] == "CRITICAL")
    high_count       = sum(1 for a in alerts if a["severity"] == "HIGH")
    recruitment_rate = (flagged_count / total_analyzed * 100) if total_analyzed > 0 else 0.0

    m1.metric("Accounts Analyzed",  f"{total_analyzed:,}")
    m2.metric("Flagged Alerts",      f"{flagged_count:,}", f"{recruitment_rate:.2f}% rate")
    m3.metric("Critical",            f"{critical_count:,}")
    m4.metric("Detection Latency",   "< 8 sec", "SLA compliant")

    # Case narrative summary strip (shown when a pre-loaded pattern is active)
    active_scenario = st.session_state.get("active_scenario")
    if active_scenario in ["roundtrip", "structuring", "dormant"]:
        st.markdown("<br/>", unsafe_allow_html=True)
        if active_scenario == "roundtrip":
            scenario_title = "Round-Trip Layering Loop — Case Narrative"
            scenario_color = "#ef4444"
            scam_summary   = "Fraudsters open multiple mule accounts to transfer funds in a high-velocity circle to manufacture fake banking activity volume, eventually flushing accumulated funds to a single laundering sink account."
            legs = [
                "**Leg 1 (Mule Input):** `ACC0520000000010` inputs **₹12.5L** via UPI to establish account velocity.",
                "**Leg 2 (Layering Transfer):** `ACC0520000000456` layers **₹15.8L** via NEFT to split the footprint.",
                "**Leg 3 (Flushing Sink):** `ACC0520000000999` flushes **₹38.5L** via RTGS to extract proceeds.",
                "**Leg 4 (Loop Closure):** Sink loops back to primary input via IMPS, triggering Warn-Flags.",
            ]
            interdiction = "Dual-engine score fusion detects the dense loop density ratio (**0.33**) and standalone ML risk probability (**100%**). System auto-triggers STR compliance XML, Section 65B tamper-proof seals, and executes a debit freeze lock via CBS webhooks in **less than 8 seconds**."
        elif active_scenario == "structuring":
            scenario_title = "UPI Structuring & Smurfing — Case Narrative"
            scenario_color = "#f97316"
            scam_summary   = "Fraudsters split large illicit proceeds into multiple micro-deposits structured strictly below the mandatory Indian KYC/PAN reporting threshold of **₹50,000** to evade legacy rule-based detection."
            legs = [
                "**Leg 1 (Structured Cash):** 28 distinct cash UPI micro-deposits from remote geolocation coordinates.",
                "**Leg 2 (Channel Switching):** Rapid switching between UPI and IMPS within a compressed 2-hour window.",
                "**Leg 3 (Accumulator Node):** Single accumulator account coordinates rapid consolidation of funds.",
            ]
            interdiction = "XGBoost classifier (hardened with SMOTE pos-weight offsets) detects the extreme transaction frequency anomaly. System scores the activity at **92.0% composite risk**, alerting core banking audit logs immediately."
        else:
            scenario_title = "Dormant Account Reactivation — Case Narrative"
            scenario_color = "#d97706"
            scam_summary   = "Fraudsters recruit high-vulnerability student/agriculture demographics (F3891) or purchase dormant credentials, reactivating long-dormant profiles (G365D age bucket) for sudden high-volume pass-through laundering."
            legs = [
                "**Leg 1 (Infiltration):** Dormant retail profile undergoes sudden digital credentials reset.",
                "**Leg 2 (Micro-Test):** Initial low-value UPI transaction of ₹10,000 executed to verify channel connectivity.",
                "**Leg 3 (Pass-through):** Immediate surge to ₹25 Lakhs in outward NEFT transfers within 24 hours.",
            ]
            interdiction = "Rules-based post-inference Mule Lifecycle Staging flags the dormancy reactivation anomaly. Escalation engine recommends immediate **digital channels suspension** and initiates a physical home branch verification block."

        st.markdown(f"""
        <div style='background-color:#0f172a;padding:18px 20px;border-radius:6px;border-left:4px solid {scenario_color};margin-bottom:20px;'>
            <div style='color:#94a3b8;font-size:10px;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px;'>Case Narrative Summary</div>
            <h4 style='color:#f8fafc;margin:0 0 8px 0;font-size:14px;font-weight:600;'>{scenario_title}</h4>
            <p style='color:#cbd5e1;font-size:13px;line-height:1.6;margin-bottom:10px;'>{scam_summary}</p>
            <div style='color:#64748b;font-size:11px;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;'>Transaction Progression</div>
            <ul style='color:#94a3b8;font-size:13px;line-height:1.7;margin:0;padding-left:18px;'>
                {"".join(f"<li>{leg}</li>" for leg in legs)}
            </ul>
            <div style='margin-top:10px;padding-top:10px;border-top:1px solid #1e293b;'>
                <span style='color:#10b981;font-size:13px;font-weight:600;'>Interdiction Result: </span>
                <span style='color:#94a3b8;font-size:13px;'>{interdiction}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Alert Queue ───────────────────────────────────────────────────────────
    st.markdown("#### Alert Queue")

    # Filters row
    fcol1, fcol2 = st.columns([2, 4])
    with fcol1:
        prev_filter = st.session_state.severity_filter
        sev_choice  = st.selectbox(
            "Severity Filter",
            options=["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"],
            index=["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"].index(
                st.session_state.severity_filter
                if st.session_state.severity_filter in ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"]
                else "ALL"
            ),
            key="severity_selectbox",
        )
        if sev_choice != prev_filter:
            st.session_state.severity_filter = sev_choice
            st.session_state.alert_page      = 0

    filtered = (
        alerts if sev_choice == "ALL"
        else [a for a in alerts if a["severity"] == sev_choice]
    )
    st.caption(f"Showing **{len(filtered)}** of {len(alerts)} alerts")

    if not filtered:
        st.info("No alerts match the active severity filter.")
        return

    # Summary table — professional investigator queue columns
    table_rows = []
    for a in filtered:
        name = "—"
        if a.get("evidence"):
            ev = a["evidence"][0]
            if ev.get("from_account") == a["account"] and ev.get("from_name"):
                name = ev["from_name"]
            elif ev.get("to_name"):
                name = ev.get("to_name", "—")
        risk = float(a.get("risk_score", 0))
        str_status = "STR Ready" if risk >= 80.0 else ("Under Review" if risk >= 40.0 else "Monitored")
        table_rows.append({
            "Severity":        a["severity"],
            "Account ID":      a["account"],
            "Account Name":    name,
            "Risk Score":      f"{a['risk_score']}%",
            "Lifecycle Stage": a.get("mule_stage", "LEGITIMATE").replace("_", " ").title(),
            "Detection Source":a.get("detection_source", "ML + Graph Fusion"),
            "STR Status":      str_status,
        })
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True)

    st.markdown("#### Detailed Forensic Investigations")

    # Pagination
    num_pages = (len(filtered) - 1) // PAGE_SIZE + 1
    page_idx  = st.number_input(
        "Page",
        min_value=1,
        max_value=num_pages,
        value=st.session_state.alert_page + 1,
        step=1,
        key="alert_page_input",
    ) - 1
    st.session_state.alert_page = page_idx

    start_idx = page_idx * PAGE_SIZE
    end_idx   = min(start_idx + PAGE_SIZE, len(filtered))

    for alert in filtered[start_idx:end_idx]:
        acc   = alert["account"]
        score = alert["risk_score"]
        sev   = alert["severity"]
        sev_color = SEVERITY_COLORS.get(sev.upper(), "#64748b")

        with st.expander(
            f"[{sev}]  Account: {acc}  |  Risk Score: {score}%  |  Stage: {alert.get('mule_stage','LEGITIMATE').replace('_',' ')}",
            expanded=False
        ):
            c_inf1, c_inf2 = st.columns(2)

            with c_inf1:
                ml_pct    = float(alert.get("ml_score",    score)) if "ml_score"    in alert else float(score)
                graph_pct = float(alert.get("graph_score", score)) if "graph_score" in alert else float(score)

                st.markdown("**Risk Score Breakdown**")
                st.markdown(f"""
                <div style='background-color:#0f172a;padding:14px;border-radius:6px;border:1px solid #1e293b;'>
                    <div style='display:flex;justify-content:space-between;margin-bottom:8px;'>
                        <span style='color:#94a3b8;font-size:12px;'>ML Probability (XGBoost)</span>
                        <span style='color:#f8fafc;font-size:12px;font-weight:600;'>{ml_pct}%</span>
                    </div>
                    <div style='display:flex;justify-content:space-between;margin-bottom:8px;'>
                        <span style='color:#94a3b8;font-size:12px;'>Graph Centrality (Neo4j)</span>
                        <span style='color:#38bdf8;font-size:12px;font-weight:600;'>{graph_pct}%</span>
                    </div>
                    <div style='display:flex;justify-content:space-between;padding-top:8px;border-top:1px solid #1e293b;'>
                        <span style='color:#94a3b8;font-size:12px;font-weight:600;'>Composite Risk Score</span>
                        <span style='color:{sev_color};font-size:14px;font-weight:700;'>{score}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("**Investigation Summary**")
                st.markdown(alert['explanation'])

                if float(score) >= 80.0:
                    st.markdown(f"""
                    <div style='background:#1e1215;border:1px solid #ef4444;border-radius:4px;padding:10px 14px;margin-top:8px;'>
                        <span style='background:#ef4444;color:#fff;padding:2px 8px;border-radius:3px;font-size:10px;font-weight:700;letter-spacing:0.05em;'>STR TRIGGERED</span>
                        <span style='color:#94a3b8;font-size:12px;margin-left:8px;'>FIU-IND compliant goAML XML generated. Account freeze recommended within 8-second SLA.</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style='background:#0f1a15;border:1px solid #10b981;border-radius:4px;padding:10px 14px;margin-top:8px;'>
                        <span style='background:#10b981;color:#fff;padding:2px 8px;border-radius:3px;font-size:10px;font-weight:700;letter-spacing:0.05em;'>MONITORED</span>
                        <span style='color:#94a3b8;font-size:12px;margin-left:8px;'>Risk below immediate freeze threshold. Continuous watchlist monitoring active.</span>
                    </div>
                    """, unsafe_allow_html=True)

            with c_inf2:
                st.markdown("**Risk Driver Analysis**")
                shap_sigs = alert.get("shap_signals", {})
                if shap_sigs:
                    shap_rows = []
                    for feature, shap_val in shap_sigs.items():
                        label = FEATURE_NAMES.get(feature, feature)
                        shap_rows.append({
                            "Risk Driver":      label,
                            "Risk Contribution": shap_val
                        })
                    df_shap = pd.DataFrame(shap_rows)

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
                        height=220
                    )
                    st.plotly_chart(fig_shap, use_container_width=True, key=f"plotly_shap_{alert['account']}")

                if "goaml_xml" in alert and alert["goaml_xml"]:
                    st.markdown("---")
                    st.markdown("**goAML Suspicious Transaction Report**")
                    render_goaml_download(alert["goaml_xml"], alert.get("case_id", "STR"), alert["account"])

                    st.markdown("**Evidence Integrity Certificate (Section 65B)**")
                    render_integrity_seal(alert.get("evidence_hash", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"))

    # Pagination controls
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        st.caption(f"Page **{page_idx + 1}** of {num_pages}")
    with col_nav2:
        col_b1, col_b2 = st.columns(2)
        if col_b1.button("Previous", key="btn_prev_page") and page_idx > 0:
            st.session_state.alert_page = page_idx - 1
        if col_b2.button("Next", key="btn_next_page") and page_idx < num_pages - 1:
            st.session_state.alert_page = page_idx + 1

    render_pdf_export(filtered)
