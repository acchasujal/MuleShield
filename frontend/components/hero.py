# frontend/components/hero.py

import streamlit as st
from frontend.components.kpi_cards import render_kpi_card

def render_hero_landing(load_scenario_callback) -> None:
    """Renders the investigation workspace landing state when no data is loaded."""
    st.markdown("#### Investigation Workspace")
    st.markdown(
        "MuleShield is a dual-engine machine learning and graph network intelligence platform "
        "for real-time identification, audit, and containment of money laundering mule accounts."
    )

    # System capability KPIs
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        render_kpi_card("Estimated Interdicted Funds",  "₹48.92 Cr",  "Benchmark dataset",          "#ef4444")
    with col_s2:
        render_kpi_card("Watchlist Nodes Synchronized", "12,852",      "Graph telemetry nodes",       "#3b82f6")
    with col_s3:
        render_kpi_card("Batch Processing SLA",         "5.81 sec",    "9,082-account benchmark",     "#f59e0b")
    with col_s4:
        render_kpi_card("Detection SLA Target",         "< 8 sec",     "Per-account interdiction",    "#10b981")

    st.markdown("<br/>", unsafe_allow_html=True)

    # Threat simulation quick-load
    st.markdown("#### Load Investigation Dataset")
    st.caption("Select a pre-loaded threat pattern to ingest transaction intelligence and activate the investigation workspace.")

    col_sc1, col_sc2, col_sc3 = st.columns(3)

    with col_sc1:
        st.markdown("""
        <div style='background-color:#0f172a;padding:16px;border-radius:6px;border:1px solid #334155;border-top:3px solid #ef4444;height:160px;'>
            <div style='display:flex;align-items:center;gap:8px;margin-bottom:8px;'>
                <span style='background:#ef4444;color:#fff;padding:1px 7px;border-radius:3px;font-size:10px;font-weight:700;'>CRITICAL</span>
            </div>
            <div style='color:#f8fafc;font-size:14px;font-weight:600;margin-bottom:6px;'>Round-Trip Layering</div>
            <p style='color:#94a3b8;font-size:12px;line-height:1.5;margin:0;'>
                High-velocity circular payment loops converging to a laundering sink account.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Load Round-Trip Dataset", key="btn_sc_roundtrip", use_container_width=True):
            load_scenario_callback("data/scenario_roundtrip.csv", "scenario_roundtrip.csv")

    with col_sc2:
        st.markdown("""
        <div style='background-color:#0f172a;padding:16px;border-radius:6px;border:1px solid #334155;border-top:3px solid #f97316;height:160px;'>
            <div style='display:flex;align-items:center;gap:8px;margin-bottom:8px;'>
                <span style='background:#f97316;color:#fff;padding:1px 7px;border-radius:3px;font-size:10px;font-weight:700;'>HIGH</span>
            </div>
            <div style='color:#f8fafc;font-size:14px;font-weight:600;margin-bottom:6px;'>Structuring / Smurfing</div>
            <p style='color:#94a3b8;font-size:12px;line-height:1.5;margin:0;'>
                Multi-leg micro-deposits structured below KYC reporting thresholds with rapid channel-switching.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Load Structuring Dataset", key="btn_sc_structuring", use_container_width=True):
            load_scenario_callback("data/scenario_structuring.csv", "scenario_structuring.csv")

    with col_sc3:
        st.markdown("""
        <div style='background-color:#0f172a;padding:16px;border-radius:6px;border:1px solid #334155;border-top:3px solid #d97706;height:160px;'>
            <div style='display:flex;align-items:center;gap:8px;margin-bottom:8px;'>
                <span style='background:#d97706;color:#fff;padding:1px 7px;border-radius:3px;font-size:10px;font-weight:700;'>MEDIUM</span>
            </div>
            <div style='color:#f8fafc;font-size:14px;font-weight:600;margin-bottom:6px;'>Dormant Reactivation</div>
            <p style='color:#94a3b8;font-size:12px;line-height:1.5;margin:0;'>
                Long-dormant accounts reactivated via social engineering for sudden high-volume pass-through flows.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Load Dormant Dataset", key="btn_sc_dormant", use_container_width=True):
            load_scenario_callback("data/scenario_dormant.csv", "scenario_dormant.csv")

    st.markdown("<br/>", unsafe_allow_html=True)

    st.markdown("#### Core Architecture")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("""
        <div style='background-color:#1e293b;padding:16px;border-radius:6px;border:1px solid #334155;'>
            <div style='color:#38bdf8;font-size:13px;font-weight:600;margin-bottom:8px;'>ML & Graph Centrality Fusion Engine</div>
            <p style='color:#94a3b8;font-size:12px;margin:0;line-height:1.6;'>
                Combines XGBoost classifiers (SMOTE 111:1 pos-weight resolution) with real-time Neo4j topological degree centrality in a 70/30 score fusion model.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_t2:
        st.markdown("""
        <div style='background-color:#1e293b;padding:16px;border-radius:6px;border:1px solid #334155;'>
            <div style='color:#10b981;font-size:13px;font-weight:600;margin-bottom:8px;'>Relational Case Auditor & Section 65B Evidence</div>
            <p style='color:#94a3b8;font-size:12px;margin:0;line-height:1.6;'>
                Judicial admissibility under Indian Evidence Act Section 65B via pre-filled goAML compliant XML reports secured with SHA-256 tamper-proof seals in PostgreSQL.
            </p>
        </div>
        """, unsafe_allow_html=True)
