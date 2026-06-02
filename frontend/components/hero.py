# frontend/components/hero.py

import streamlit as st
from frontend.components.kpi_cards import render_kpi_card

def render_hero_landing(load_scenario_callback) -> None:
    """Renders the landing console interface when no files are loaded."""
    st.markdown("### 🛡️ Welcome to MuleShield AI Security Command Console")
    st.markdown("""
    *MuleShield AI is a state-of-the-art dual-engine machine learning and graph network intelligence terminal engineered to identify, audit, and freeze money laundering mule accounts in real-time.*
    """)
    
    # Premium Stats Cards Row
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        render_kpi_card("Estimated Prevented Loss", "₹48.92 Cr", "🛡️ Interdicted Funds (Est.)", "#ef4444")
    with col_s2:
        render_kpi_card("Est. Watchlist Telemetry", "12,852", "🔗 Graph Nodes (Est.)", "#3b82f6")
    with col_s3:
        render_kpi_card("Batch Processing SLA", "5.81 sec", "⚡ 9,082 Accounts Benchmark", "#f59e0b")
    with col_s4:
        render_kpi_card("Detection SLA Target", "< 8 sec", "⚡ Per-Account Latency", "#10b981")
        
    st.markdown("<br/>", unsafe_allow_html=True)
    
    st.markdown("### ⚡ Live Sandbox Demo Scenario Launchpad")
    st.caption("Click any high-fidelity scenario card directly to ingest the transaction alerts and launch the Story-Guided Demo Portal.")
    
    col_sc1, col_sc2, col_sc3 = st.columns(3)
    
    with col_sc1:
        st.markdown("""
        <div style='background-color:#0f172a;padding:15px;border-radius:8px;border:1px solid #ef4444;height:180px;box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1);'>
            <h4 style='color:#f8fafc;margin:0 0 10px 0;font-size:16px;'>🔁 Round-Trip Layering</h4>
            <p style='color:#94a3b8;font-size:12px;line-height:1.4;'>
                Scans for high-velocity transaction loops structured using multiple circular payment transfers closing at a single laundering sink.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔁 Load Round-Trip Scenario", key="btn_sc_roundtrip", use_container_width=True):
            load_scenario_callback("data/scenario_roundtrip.csv", "scenario_roundtrip.csv")
            
    with col_sc2:
        st.markdown("""
        <div style='background-color:#0f172a;padding:15px;border-radius:8px;border:1px solid #f97316;height:180px;box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1);'>
            <h4 style='color:#f8fafc;margin:0 0 10px 0;font-size:16px;'>💰 Structuring / Smurfing</h4>
            <p style='color:#94a3b8;font-size:12px;line-height:1.4;'>
                Detects multi-leg micro-deposits structured below reporting thresholds via rapid payment channel-switching.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💰 Load Structuring Scenario", key="btn_sc_structuring", use_container_width=True):
            load_scenario_callback("data/scenario_structuring.csv", "scenario_structuring.csv")
            
    with col_sc3:
        st.markdown("""
        <div style='background-color:#0f172a;padding:15px;border-radius:8px;border:1px solid #eab308;height:180px;box-shadow:0 4px 6px -1px rgb(0 0 0 / 0.1);'>
            <h4 style='color:#f8fafc;margin:0 0 10px 0;font-size:16px;'>💤 Dormant Reactivation</h4>
            <p style='color:#94a3b8;font-size:12px;line-height:1.4;'>
                Tracks long-sleeping student/agriculture accounts purchased by syndicates and instantly reactivated for pass-through flows.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💤 Load Dormant Scenario", key="btn_sc_dormant", use_container_width=True):
            load_scenario_callback("data/scenario_dormant.csv", "scenario_dormant.csv")
            
    st.markdown("<br/>", unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Core Architecture Technical Specifications")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("""
        <div style='background-color:#1e293b;padding:15px;border-radius:8px;border:1px solid #334155;height:140px;'>
            <b style='color:#38bdf8;'>🧠 Tabular ML & Graph Centrality Fusion Engine</b>
            <p style='color:#94a3b8;font-size:12px;margin-top:8px;line-height:1.4;'>
                Combines positive imbalanced-resolution XGBoost classifiers (trained with dynamic SMOTE 111:1 pos-weights) with real-time Neo4j topological degree centrality lookups in a 70/30 score fusion SLA model.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_t2:
        st.markdown("""
        <div style='background-color:#1e293b;padding:15px;border-radius:8px;border:1px solid #334155;height:140px;'>
            <b style='color:#10b981;'>🔐 Relational Case Auditor & Section 65B OpenTimestamps</b>
            <p style='color:#94a3b8;font-size:12px;margin-top:8px;line-height:1.4;'>
                Ensures judicial admissibility under Indian Evidence Act Section 65B by automatically generating pre-filled goAML compliant XML reports secured with SHA-256 tamper-proof seals in PostgreSQL databases.
            </p>
        </div>
        """, unsafe_allow_html=True)
