# frontend/components/demo_mode.py

import pandas as pd
import streamlit as st

def render_demo_mode_view(load_scenario_callback) -> None:
    """Renders the Sandbox Demo Mode interface."""
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);padding:30px;border-radius:12px;border:1px solid #38bdf8;margin-bottom:24px;box-shadow:0 8px 32px rgba(56,189,248,0.1);'>
        <h2 style='color:#f8fafc;margin:0 0 8px 0;font-size:26px;'>🎮 MuleShield AI — Live Sandbox Demo Mode</h2>
        <p style='color:#94a3b8;margin:0;font-size:14px;line-height:1.6;'>
            Click any scenario card below to instantly launch a high-fidelity money laundering simulation.
            No file uploads. No configuration. No typing required.
            The system automatically ingests pre-generated transaction intelligence and activates the Story-Guided Portal.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Active scenario indicator
    active_scenario = st.session_state.get("active_scenario")
    if active_scenario and st.session_state.analysis_result is not None:
        scenario_labels = {
            "roundtrip": ("🔁 Round-Trip Layering Loop", "#ef4444"),
            "structuring": ("💰 UPI Structuring / Smurfing", "#f97316"),
            "dormant": ("💤 Dormant Account Reactivation", "#eab308"),
        }
        lbl, clr = scenario_labels.get(active_scenario, ("Unknown", "#94a3b8"))
        alerts_loaded = len(st.session_state.analysis_result.get("alerts", []))
        st.markdown(f"""
        <div style='background-color:#0f172a;padding:14px 20px;border-radius:8px;border-left:5px solid {clr};margin-bottom:20px;display:flex;align-items:center;gap:12px;'>
            <span style='color:{clr};font-size:20px;'>✅</span>
            <div>
                <span style='color:#f8fafc;font-weight:bold;font-size:15px;'>{lbl} — Loaded</span><br/>
                <span style='color:#94a3b8;font-size:12px;'>{alerts_loaded} suspicious accounts flagged. Switch to 🕵️ Alert Center to investigate.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        col_go1, col_go2 = st.columns([1, 3])
        with col_go1:
            if st.button("🕵️ Go to Alert Center →", key="demo_goto_alerts", use_container_width=True):
                st.session_state.demo_mode_active = True
                st.rerun()

    st.markdown("### 🚀 Choose a Scenario to Launch")
    st.caption("Each scenario is backed by synthetically-generated transaction data matching real-world AML laundering patterns.")

    # Scenario Cards
    col_d1, col_d2, col_d3 = st.columns(3)

    with col_d1:
        st.markdown("""
        <div style='background:#0f172a;padding:20px;border-radius:10px;border:1px solid #ef4444;min-height:280px;box-shadow:0 4px 20px rgba(239,68,68,0.15);'>
            <div style='font-size:28px;margin-bottom:8px;'>🔁</div>
            <h4 style='color:#f8fafc;margin:0 0 6px 0;font-size:16px;'>Round-Trip Layering Loop</h4>
            <p style='color:#94a3b8;font-size:12px;line-height:1.5;margin-bottom:12px;'>
                Multi-mule circular RTGS/UPI fund loop with a laundering sink account. Detects dense graph topology and velocity anomalies.
            </p>
            <div style='background:#1e293b;padding:10px;border-radius:6px;margin-bottom:12px;'>
                <div style='color:#ef4444;font-size:11px;font-weight:bold;text-transform:uppercase;margin-bottom:4px;'>Attack Pattern</div>
                <div style='color:#94a3b8;font-size:11px;line-height:1.6;'>
                    Input A → Input B → Input C<br/>
                    ↓ (all converge) ↓<br/>
                    🎯 Sink: ₹38.5L RTGS<br/>
                    ↩ Loop back via IMPS
                </div>
            </div>
            <div style='display:flex;gap:6px;flex-wrap:wrap;'>
                <span style='background:#ef4444;color:white;padding:2px 8px;border-radius:12px;font-size:10px;font-weight:bold;'>CRITICAL</span>
                <span style='background:#1e293b;color:#94a3b8;padding:2px 8px;border-radius:12px;font-size:10px;'>Neo4j Graph</span>
                <span style='background:#1e293b;color:#94a3b8;padding:2px 8px;border-radius:12px;font-size:10px;'>RTGS/UPI</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔁 Launch Round-Trip Demo", key="dm_launch_roundtrip", use_container_width=True):
            with st.spinner("⚡ Loading Round-Trip Layering simulation..."):
                load_scenario_callback("data/scenario_roundtrip.csv", "scenario_roundtrip.csv")
            st.session_state.demo_mode_active = True
            st.rerun()

    with col_d2:
        st.markdown("""
        <div style='background:#0f172a;padding:20px;border-radius:10px;border:1px solid #f97316;min-height:280px;box-shadow:0 4px 20px rgba(249,115,22,0.15);'>
            <div style='font-size:28px;margin-bottom:8px;'>💰</div>
            <h4 style='color:#f8fafc;margin:0 0 6px 0;font-size:16px;'>UPI Structuring / Smurfing</h4>
            <p style='color:#94a3b8;font-size:12px;line-height:1.5;margin-bottom:12px;'>
                28 micro-deposits below ₹50,000 KYC threshold via rapid UPI↔IMPS channel-switching to evade rule-based detection.
            </p>
            <div style='background:#1e293b;padding:10px;border-radius:6px;margin-bottom:12px;'>
                <div style='color:#f97316;font-size:11px;font-weight:bold;text-transform:uppercase;margin-bottom:4px;'>Attack Pattern</div>
                <div style='color:#94a3b8;font-size:11px;line-height:1.6;'>
                    28× UPI ₹49,999 deposits<br/>
                    ↓ Channel Switch: UPI→IMPS<br/>
                    ↓ Consolidator node<br/>
                    🎯 Bulk NEFT withdrawal
                </div>
            </div>
            <div style='display:flex;gap:6px;flex-wrap:wrap;'>
                <span style='background:#f97316;color:white;padding:2px 8px;border-radius:12px;font-size:10px;font-weight:bold;'>HIGH</span>
                <span style='background:#1e293b;color:#94a3b8;padding:2px 8px;border-radius:12px;font-size:10px;'>SMOTE Detection</span>
                <span style='background:#1e293b;color:#94a3b8;padding:2px 8px;border-radius:12px;font-size:10px;'>UPI/IMPS</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💰 Launch Structuring Demo", key="dm_launch_structuring", use_container_width=True):
            with st.spinner("⚡ Loading Structuring / Smurfing simulation..."):
                load_scenario_callback("data/scenario_structuring.csv", "scenario_structuring.csv")
            st.session_state.demo_mode_active = True
            st.rerun()

    with col_d3:
        st.markdown("""
        <div style='background:#0f172a;padding:20px;border-radius:10px;border:1px solid #eab308;min-height:280px;box-shadow:0 4px 20px rgba(234,179,8,0.15);'>
            <div style='font-size:28px;margin-bottom:8px;'>💤</div>
            <h4 style='color:#f8fafc;margin:0 0 6px 0;font-size:16px;'>Dormant Account Reactivation</h4>
            <p style='color:#94a3b8;font-size:12px;line-height:1.5;margin-bottom:12px;'>
                Fraudsters recruit G365D age-bucket dormant student/agri profiles via social engineering for sudden high-volume pass-through laundering.
            </p>
            <div style='background:#1e293b;padding:10px;border-radius:6px;margin-bottom:12px;'>
                <div style='color:#eab308;font-size:11px;font-weight:bold;text-transform:uppercase;margin-bottom:4px;'>Attack Pattern</div>
                <div style='color:#94a3b8;font-size:11px;line-height:1.6;'>
                    Dormant profile reset<br/>
                    ↓ Test: ₹10,000 UPI<br/>
                    ↓ Surge: ₹25L NEFT within 24h<br/>
                    🎯 Digital channel block
                </div>
            </div>
            <div style='display:flex;gap:6px;flex-wrap:wrap;'>
                <span style='background:#eab308;color:black;padding:2px 8px;border-radius:12px;font-size:10px;font-weight:bold;'>MEDIUM</span>
                <span style='background:#1e293b;color:#94a3b8;padding:2px 8px;border-radius:12px;font-size:10px;'>F3889 Rule</span>
                <span style='background:#1e293b;color:#94a3b8;padding:2px 8px;border-radius:12px;font-size:10px;'>G365D Bucket</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("💤 Launch Dormant Demo", key="dm_launch_dormant", use_container_width=True):
            with st.spinner("⚡ Loading Dormant Reactivation simulation..."):
                load_scenario_callback("data/scenario_dormant.csv", "scenario_dormant.csv")
            st.session_state.demo_mode_active = True
            st.rerun()

    st.markdown("<br/>", unsafe_allow_html=True)

    # Inline results preview when scenario is loaded
    if st.session_state.analysis_result is not None:
        st.markdown("---")
        st.markdown("### 📊 Quick Results Preview")
        st.caption("Scenario analysis complete. Explore full details in the Alert Center or Account Inspector.")
        result = st.session_state.analysis_result
        alerts = result.get("alerts", [])
        flagged = result.get("flagged_count", len(alerts))
        total = result.get("total_analyzed", flagged)

        prv1, prv2, prv3, prv4 = st.columns(4)
        prv1.metric("📁 Ingested Accounts", f"{total:,}")
        prv2.metric("🚨 Flagged Mule Alerts", f"{flagged:,}")
        critical_c = sum(1 for a in alerts if a.get("severity") == "CRITICAL")
        prv3.metric("🔥 Critical Escalations", f"{critical_c:,}")
        prv4.metric("⚡ Detection Latency", "< 8 sec", "SLA ✅")

        if alerts:
            st.markdown("#### 🔴 Top Flagged Accounts")
            top_rows = []
            for a in alerts[:6]:
                top_rows.append({
                    "Account ID": a.get("account", "—"),
                    "Composite Risk": f"{a.get('risk_score', 0)}%",
                    "Severity": a.get("severity", "LOW"),
                    "Mule Stage": a.get("mule_stage", "LEGITIMATE"),
                })
            st.dataframe(pd.DataFrame(top_rows), width='stretch')

        col_nav_d1, col_nav_d2 = st.columns(2)
        with col_nav_d1:
            st.info("👆 Switch to **🕵️ Alert Center** in the sidebar to explore full forensic investigations.")
        with col_nav_d2:
            st.info("🔍 Switch to **🔍 Account Inspector** to run deep XAI profiling on individual accounts.")
